from __future__ import annotations

import json
import time
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any, Dict, Literal

from neo4j import GraphDatabase, Query
from neo4j.exceptions import Neo4jError

from src.logger_config import setup_logger

logger = setup_logger(__name__)


class Neo4jConnector:
    def __init__(
        self,
        host: str,
        port: int,
        username: str,
        password: str,
        database: str = "neo4j",
        name: str = "neo4j-db",
        max_connection_pool_size: int = 100,
        debug: bool = False,
    ):
        """Neo4j connector for query execution and dataset import."""
        self.name = name
        self.database = database
        self.debug = debug

        connection_uri = f"{host}:{port}"
        logger.info("Connecting to Neo4j at: %s", connection_uri)

        self.driver = GraphDatabase.driver(
            connection_uri,
            auth=(username, password),
            max_connection_pool_size=max_connection_pool_size,
        )

    def close(self):
        if getattr(self, "driver", None) is not None:
            self.driver.close()

    def run_query(
        self,
        cypher: str,
        timeout: int | None = None,
        convert_func: Literal["data", "graph"] = "data",
        **kwargs,
    ):
        if self.debug:
            t0 = time.time()
            logger.info("Running Cypher:\n%s", cypher)
        try:
            with self.driver.session(database=self.database) as session:
                query = Query(cypher, timeout=timeout)
                result = session.run(query, **kwargs)

                if convert_func == "data":
                    output = result.data()
                elif convert_func == "graph":
                    output = result.graph()
                else:
                    raise ValueError(f"Invalid convert_func: {convert_func}")
        except Exception:
            logger.error("ERROR when executing Cypher: %s", cypher)
            raise

        if self.debug:
            logger.info("Query finished in %.2fs", time.time() - t0)
        return output

    def run_query_advance(
        self,
        cypher: str,
        *,
        timeout: int | None = None,
        convert_func: Literal["list", "data", "graph"] = "list",
        **kwargs,
    ) -> Dict[str, Any]:
        if self.debug:
            logger.info("==== RUN QUERY ====")
            logger.info(cypher)
            logger.info("Params: %s", kwargs)
            t0 = time.time()

        try:
            with self.driver.session(database=self.database) as session:
                query = Query(cypher, timeout=timeout)
                result = session.run(query, **kwargs)

                if convert_func == "list":
                    records = [dict(r) for r in result]
                elif convert_func == "data":
                    records = result.data()
                elif convert_func == "graph":
                    records = result.graph()
                else:
                    raise ValueError("Invalid convert_func")

                summary = result.consume()
                status_objects = getattr(summary, "gql_status_objects", None) or []

                notifications = []
                has_error = False
                for note in status_objects:
                    severity = getattr(
                        getattr(note, "severity", None), "name", "UNKNOWN"
                    )
                    notifications.append(
                        {
                            "severity": severity,
                            "gql_status": getattr(note, "gql_status", None),
                            "description": getattr(note, "status_description", None),
                            "position": {
                                "line": getattr(
                                    getattr(note, "position", None), "line", None
                                ),
                                "column": getattr(
                                    getattr(note, "position", None), "column", None
                                ),
                                "offset": getattr(
                                    getattr(note, "position", None), "offset", None
                                ),
                            },
                            "classification": str(
                                getattr(note, "classification", None)
                            ),
                            "raw_classification": getattr(
                                note, "raw_classification", None
                            ),
                        }
                    )
                    if severity in {"ERROR", "FATAL", "WARNING"}:
                        has_error = True

                if self.debug:
                    logger.info("Query finished in %.3fs", time.time() - t0)
                    if notifications:
                        logger.warning("Notifications: %s", notifications)

                return {
                    "success": not has_error,
                    "records": records,
                    "notifications": notifications,
                }
        except Exception as e:
            logger.error("ERROR when executing Cypher: %s", cypher)
            return {
                "success": False,
                "records": [],
                "notifications": [{"severity": "EXCEPTION", "description": str(e)}],
            }

    def get_num_entities(self) -> int:
        return self.run_query("MATCH (n) RETURN count(n) as num")[0]["num"]

    def get_num_relations(self) -> int:
        return self.run_query("MATCH ()-[r]->() RETURN count(r) as num")[0]["num"]

    def wait_for_db_online(self, db_name: str, timeout: int = 10):
        """Wait until the target database status is online."""
        with self.driver.session(database="system") as session:
            start = time.time()
            while True:
                dbs = session.run("SHOW DATABASES").data()
                for db in dbs:
                    if (
                        db["name"] == db_name
                        and db["currentStatus"].lower() == "online"
                    ):
                        logger.info("Database '%s' is online", db_name)
                        return
                if time.time() - start > timeout:
                    raise TimeoutError(
                        f"Database '{db_name}' not online after {timeout} seconds"
                    )
                time.sleep(0.5)

    def create_or_reset_db(self, db_name: str, overwrite: bool):
        """
        Create DB if not exist.
        If overwrite=True:
        - Enterprise: DROP/CREATE database.
        - Community: clear all data with DETACH DELETE.
        """
        try:
            with self.driver.session(database="system") as session:
                dbs = session.run("SHOW DATABASES").data()
                exists = any(db["name"] == db_name for db in dbs)

                if exists and overwrite:
                    try:
                        logger.info(
                            "Dropping existing database: '%s' (Enterprise)", db_name
                        )
                        session.run(f"DROP DATABASE {db_name} IF EXISTS")
                        session.run(f"CREATE DATABASE {db_name}")
                        return
                    except Neo4jError as e:
                        if "UnsupportedAdministrationCommand" not in str(e):
                            raise
                        logger.info(
                            "Enterprise DB admin unsupported, fallback to Community mode"
                        )
                elif not exists:
                    try:
                        logger.info("Creating database: '%s'", db_name)
                        session.run(f"CREATE DATABASE {db_name}")
                        return
                    except Neo4jError as e:
                        if "UnsupportedAdministrationCommand" not in str(e):
                            raise
                        logger.info(
                            "CREATE DATABASE unsupported, fallback to Community mode"
                        )
                else:
                    logger.info(
                        "Database '%s' already exists (overwrite=False)", db_name
                    )
                    return
        except Exception as e:
            logger.warning("Cannot use system database commands, fallback mode: %s", e)

        if overwrite:
            logger.info("Clearing all data in database '%s' (Community mode)", db_name)
            with self.driver.session(database=db_name) as session:
                session.run("MATCH (n) DETACH DELETE n")

    @staticmethod
    def apply_schema_constraints(session, schema: dict):
        """Create unique eid constraints for all entity labels."""
        unique_labels = {e["label"] for e in schema.get("entities", [])}
        for label in unique_labels:
            session.run(
                f"""
                CREATE CONSTRAINT IF NOT EXISTS
                FOR (n:`{label}`)
                REQUIRE n.eid IS UNIQUE
                """
            )
            logger.info("Constraint ensured for label '%s'", label)

    @staticmethod
    def import_entities(session, entities: list[dict], batch_size: int = 5000):
        """Import entities grouped by label, in batches."""
        grouped = defaultdict(list)
        for ent in entities:
            grouped[ent["label"]].append(
                {
                    "eid": ent["eid"],
                    "name": ent.get("name"),
                    "aliases": ent.get("aliases", []),
                    "description": ent.get("description"),
                    "provenance": ent.get("provenance", []),
                    "properties": ent.get("properties", {}),
                }
            )

        query_tpl = """
        UNWIND $batch AS row
        MERGE (n:`{label}` {{eid: row.eid}})
        SET
            n.name = row.name,
            n.aliases = row.aliases,
            n.description = row.description,
            n.provenance = row.provenance
        SET n += row.properties
        """

        for label, rows in grouped.items():
            cypher = query_tpl.format(label=label)
            for i in range(0, len(rows), batch_size):
                session.run(cypher, batch=rows[i : i + batch_size])
            logger.info("Imported %d entities [%s]", len(rows), label)

    @staticmethod
    def build_label_mapping(schema: dict) -> dict:
        """
        Build relation label mapping from schema:
        relation.label -> {"source": subj_label, "target": obj_label}
        """
        return {
            r["label"]: {"source": r["subj_label"], "target": r["obj_label"]}
            for r in schema.get("relations", [])
            if "subj_label" in r and "obj_label" in r
        }

    def _import_relations_single_label(
        self,
        db_name: str,
        label: str,
        relations: list[dict],
        source_label: str,
        target_label: str,
        batch_size: int = 5000,
        use_create: bool = True,
    ):
        rel_clause = "CREATE" if use_create else "MERGE"
        cypher = f"""
        UNWIND $batch AS row
        MATCH (s:`{source_label}` {{eid: row.subj}})
        MATCH (o:`{target_label}` {{eid: row.obj}})
        {rel_clause} (s)-[r:`{label}`]->(o)
        SET r += row.properties,
            r.provenance = row.provenance
        """

        with self.driver.session(database=db_name) as session:
            tx = session.begin_transaction()
            try:
                for i in range(0, len(relations), batch_size):
                    tx.run(cypher, batch=relations[i : i + batch_size])
                    tx.commit()
                    tx = session.begin_transaction()
                tx.commit()
            except Exception:
                tx.rollback()
                raise

        logger.info("Imported %d relations [%s]", len(relations), label)

    @staticmethod
    def _import_relations_without_mapping(
        session, relations: list[dict], batch_size: int = 1000
    ):
        """Fallback relation import when source/target labels are unknown."""
        grouped = defaultdict(list)
        for rel in relations:
            grouped[rel["label"]].append(
                {
                    "subj": rel["subj_id"],
                    "obj": rel["obj_id"],
                    "properties": rel.get("properties", {}),
                    "provenance": rel.get("provenance", []),
                }
            )

        for label, rows in grouped.items():
            cypher = f"""
            UNWIND $batch AS row
            MATCH (s {{eid: row.subj}})
            MATCH (o {{eid: row.obj}})
            MERGE (s)-[r:`{label}`]->(o)
            SET r += row.properties,
                r.provenance = row.provenance
            """
            for i in range(0, len(rows), batch_size):
                session.run(cypher, batch=rows[i : i + batch_size])
            logger.info("Imported %d relations [%s] (fallback)", len(rows), label)

    def import_relations(
        self,
        relations: list[dict],
        db_name: str | None = None,
        label_mapping: dict | None = None,
        batch_size: int = 5000,
        max_workers: int = 4,
        use_create: bool = True,
    ):
        """
        Import relationships.
        - If label_mapping is provided: import by relation type in parallel with strict source/target labels.
        - Else: fallback import using eid-only matching.
        """
        db = db_name or self.database
        if not relations:
            return

        if not label_mapping:
            with self.driver.session(database=db) as session:
                self._import_relations_without_mapping(
                    session, relations, batch_size=batch_size
                )
            return

        grouped = defaultdict(list)
        for rel in relations:
            grouped[rel["label"]].append(
                {
                    "subj": rel["subj_id"],
                    "obj": rel["obj_id"],
                    "properties": rel.get("properties", {}),
                    "provenance": rel.get("provenance", []),
                }
            )

        tasks = []
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            for label, rows in grouped.items():
                mapping = label_mapping.get(label)
                if not mapping:
                    logger.warning(
                        "Missing mapping for relation label '%s', skipping", label
                    )
                    continue
                tasks.append(
                    executor.submit(
                        self._import_relations_single_label,
                        db,
                        label,
                        rows,
                        mapping["source"],
                        mapping["target"],
                        batch_size,
                        use_create,
                    )
                )
            for future in as_completed(tasks):
                future.result()

    def import_json_dataset(
        self,
        filepath: str,
        db_name: str | None = None,
        overwrite: bool = False,
        batch_size: int = 1000,
        entity_batch: int | None = None,
        rel_batch: int | None = None,
        max_workers: int = 4,
        relation_label_mapping: dict | None = None,
        use_create: bool = True,
    ):
        """
        Full import pipeline from JSON.

        Compatibility:
        - Supports old signature using batch_size only.
        - Supports advanced signature with entity_batch/rel_batch and relation_label_mapping.
        """
        db = db_name or self.database
        entity_bs = entity_batch or batch_size
        rel_bs = rel_batch or batch_size
        start_time = time.time()

        logger.info("Loading JSON dataset from: %s", filepath)
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        schema = data["schema"]
        entities = data["entities"]
        relations = data["relations"]
        label_mapping = relation_label_mapping or self.build_label_mapping(schema)

        logger.info(
            "Dataset loaded: %d entities, %d relations", len(entities), len(relations)
        )

        self.create_or_reset_db(db, overwrite)
        self.wait_for_db_online(db)

        with self.driver.session(database=db) as session:
            self.apply_schema_constraints(session, schema)
            self.import_entities(session, entities, batch_size=entity_bs)

        self.import_relations(
            relations,
            db_name=db,
            label_mapping=label_mapping,
            batch_size=rel_bs,
            max_workers=max_workers,
            use_create=use_create,
        )

        logger.info("IMPORT DONE into DB '%s' in %.2fs", db, time.time() - start_time)
