# Representative 50-sample subset for the first two taxonomy columns

The subset matches the nearest feasible integer counts implied by the full 2,348-query rates. Selection uses only the two requested marginal labels.

| Method | Full Schema | 50-sample Schema | Δ pp | Full Graph | 50-sample Graph | Δ pp |
|---|---:|---:|---:|---:|---:|---:|
| Qwen3-4B (Teacher) | 383 (16.31%) | 8 (16.00%) | -0.31 | 511 (21.76%) | 11 (22.00%) | +0.24 |
| Qwen3-0.6B (SFT) | 1026 (43.70%) | 22 (44.00%) | +0.30 | 568 (24.19%) | 12 (24.00%) | -0.19 |
| CSD | 671 (28.58%) | 14 (28.00%) | -0.58 | 581 (24.74%) | 12 (24.00%) | -0.74 |
| DistiLLM | 691 (29.43%) | 15 (30.00%) | +0.57 | 562 (23.94%) | 12 (24.00%) | +0.06 |
| CypherKD | 630 (26.83%) | 13 (26.00%) | -0.83 | 554 (23.59%) | 12 (24.00%) | +0.41 |

## Selected cases

| # | Graph / local index | QID | Question |
|---:|---|---|---|
| 1 | company #14 | `45f852bc-4ee8-4233-b36e-d3584f6b63a2` | What are the names of industries in which Canadian companies operate, and how many Canadian companies are there in each industry? |
| 2 | company #40 | `f62f09d8-7e16-4c01-a8a8-ebac7d043c24` | What are the unique countries of citizenship of individuals who have both served as CEO and founded a company? |
| 3 | company #45 | `6a6299a7-86eb-497e-8f57-958a0f0d7290` | Which country is BFM DICI Haute-Provence based? |
| 4 | company #85 | `14c72f2e-097e-4073-9348-3e90e49c1b4a` | What are the names of companies that have shared a CEO with CDP Reti at some point in time? |
| 5 | company #124 | `a26fa1a8-6f9a-4f0c-9500-69b2c4d9de8a` | Who are the founders of companies that are subsidiaries of HSBC? |
| 6 | company #147 | `d6aa121b-59b4-4892-a087-d5806cacf86a` | Provide the names of all companies located in Russia, along with the number of individuals who have served on their boards at any time. |
| 7 | company #216 | `14133f73-936a-474a-bcac-f9713b86d64d` | Who are the individuals that Tennman Records was founded by, and where were they born? |
| 8 | company #251 | `d5bf7668-3d2c-4177-9519-17c9e41408cb` | Which companies had Hartmut Mehdorn as their CEO during the year 2009? |
| 9 | company #263 | `a8ed414d-86b8-4f2d-a1ef-2c45df64661c` | What are the names of companies that operate in the hospitality industry and are subsidiaries of Raffles Hotels & Resorts? |
| 10 | fictional_character #149 | `de10f3bb-755e-465f-9f03-cf84d0c36d55` | What are the names of organizations that have members born in Asgard, and how many such members does each organization have? |
| 11 | fictional_character #196 | `0f9a6d6e-e581-449a-9380-17a330274f35` | Provide the names of all children of Joanna Lannister, along with the count of characters each of them have killed. |
| 12 | fictional_character #255 | `8672e6ed-73e8-4ff6-bd7c-262f194a623d` | What are the names of characters whose father is the Grandfather of the Troublemaker Street children and whose mother is the Grandmother of the Troublemaker Street children? |
| 13 | fictional_character #261 | `39583118-e09c-4862-8712-fa44983386e5` | What are the names of individuals who are fathers and are citizens of the United States of America? |
| 14 | fictional_character #264 | `dd71c7fc-c4a9-46a6-a262-b531b016baff` | Provide the names of all characters from the Futuramaverse and, for each, the number of organizations each of them belongs to. |
| 15 | fictional_character #308 | `e17375b6-af03-4866-8d42-6e824098acbd` | What are the names of characters from Earth-167 who were born on Krypton and are not murderers by occupation? |
| 16 | fictional_character #347 | `0035a8ec-c55b-47a5-9429-ca74b117f86f` | Provide the names of all characters whose mother is Downy O'Drake, along with the count of characters for whom each is the father. |
| 17 | fictional_character #368 | `54ebd630-30f2-4da4-997c-02a9d37ad463` | How many characters are either the father of Zhao Guang or killed Su Yong? |
| 18 | flight_accident #87 | `7b450f61-fad7-4ca7-b408-1a6ebdfc098a` | What is the ICAO code for Iwakuni Air Base? |
| 19 | flight_accident #184 | `c54b9f25-1d3b-4df6-88e8-bd37b9eb305e` | What year was the Ulan-Ude Aviation Plant launched? |
| 20 | geography #42 | `5f2d6d46-ba37-494b-b0f0-636b5d4f780d` | What are the names of countries where lakes that the Yuan River flows into are located? |
| 21 | geography #54 | `1ab6cb26-4424-433d-82df-978caf0eed5b` | What are the names of countries where either Lac la Ronge or the Rivière du Lièvre basin is located? |
| 22 | geography #56 | `7926da80-d841-48ba-944d-051b221bf21d` | What are the names of countries through which both the Bolshoy Kunyak and Katiss rivers flow? |
| 23 | geography #70 | `4d4a75cb-6449-424e-aaba-1ff7057f0dd9` | What are the names of countries through which a river flowing through Cameroon also passes, sorted by their area from largest to smallest? |
| 24 | geography #94 | `8b14ae44-657a-4aab-881c-050bebd2351f` | What are the names of lakes located in the Democratic Republic of the Congo, and how many drainage basins is each one part of? |
| 25 | geography #120 | `aa6a132d-f296-4e20-8471-728ff27e28bc` | What are the names of countries in which either the Saint Lawrence River basin or Batiscanie is located? |
| 26 | geography #147 | `634b1a5c-2951-4285-8b1a-2fb757d2c4af` | What are the names of drainage basins that are located in the same countries as the Vorskla River Basin, and how many of those countries does each basin span? |
| 27 | geography #167 | `937960b0-405e-4b46-ae54-7e64dc90eb03` | What are the names of the mountain ranges that include Uja Tirche? |
| 28 | geography #183 | `36142220-fe13-46d9-820a-612571ec0ed9` | What are the names of lakes that are situated in both Turkmenistan and Kazakhstan? |
| 29 | movie #15 | `8163f80b-8323-4300-9697-1910ded21b18` | What are the names and original languages of action films produced by Relativity Media? |
| 30 | movie #52 | `861aace7-0d68-466a-91f3-73d3818318f6` | How many movies were either released in Australia or produced by Bazmark? |
| 31 | movie #77 | `baec6063-e583-406a-929f-55ed823113cd` | What is the difference in runtime, in minutes, between The Long Way Home and The Father? |
| 32 | movie #149 | `c6cf9227-8fcf-4cbf-a318-040316af1671` | What are the names of movies featuring either Jon Favreau or Martha Kelly? |
| 33 | movie #252 | `f63c99e3-a10c-4ede-8563-4fa684e94e12` | What are the names of all movies that are part of the Alien series, and how many cast members does each have? |
| 34 | movie #263 | `b4f0b743-7317-4d45-b8cf-1db0b0c51d29` | How many production companies have produced movies that received the Satellite Award for Best Original Screenplay? |
| 35 | movie #278 | `2816b588-b849-4c46-9c4a-26d483f162bc` | Who are the directors of movies featuring Minae Noji? |
| 36 | movie #290 | `0f254d81-0d68-4df5-bfa4-0d8ea58c9503` | What are the awards received by the movie Caché? |
| 37 | movie #397 | `5af3bdd8-4ab8-4cb5-9e0c-6dfff3268844` | What are the names of movies produced by Media Cooperation One, along with their global box office earnings in USD? |
| 38 | nba #33 | `047e97cb-44fb-4148-b36e-c539e0340d16` | What are the names of awards received by players who play the small forward position? |
| 39 | nba #98 | `6ca84420-ea44-44aa-b31f-d373bf45f0ae` | Who are the players who have been on the same teams as Aron Baynes, and how many of those teams has each player been a part of? |
| 40 | nba #151 | `c21c5900-7028-4de2-a792-1459cf645449` | What are the names and owners of teams that drafted Kent Benson and have Jabari Parker as a player, either currently or in the past? |
| 41 | nba #195 | `f29c01d9-fb9f-4384-b5fa-77a0538d9943` | What are the names of divisions that are part of the Western Conference and include the Sacramento Kings? |
| 42 | nba #205 | `df3389b0-1ba2-4dea-9216-b1c5eabd79e8` | What are the names of teams that are in the same division as the New Orleans Pelicans? |
| 43 | politics #43 | `8ecf34fe-ee65-4c97-9f12-980ed78ef03c` | How many countries does the Federal Reserve System belong to, or have diplomatic relations with South Korea? |
| 44 | politics #72 | `0df01cfe-6dc3-47c7-8ed1-540d0ce23de0` | Which country, having had the same politician serve as both head of government and head of state at some point, was founded the earliest? |
| 45 | politics #86 | `93105d1f-0e28-4303-830b-acdcbf668ef7` | How many countries have either had Walter Scheel as their head of state at some point or have diplomatic relations with East Timor? |
| 46 | politics #88 | `a3d7c6c3-11bc-446b-819b-bb42a573a4df` | What are the names of political parties that include members who were founders of The Patriots? |
| 47 | politics #116 | `0a6ef5c9-1bac-44bd-82c7-8ae01f5f88c6` | Who are the politicians who have held any of the same positions as Ivan Konev, and how many of those positions has each of them held? |
| 48 | politics #248 | `82d404e2-5b52-47af-8247-6074d9992ae6` | What are the names of politicians who have served as both head of government and head of state for a country, sorted by their date of death from earliest to latest? |
| 49 | politics #250 | `68f81304-b81d-4981-8640-e7940503624c` | What are the names of politicians who have served as either the head of state or head of government of Germany, at any time? |
| 50 | politics #345 | `bdbe3528-5bb6-4e06-ac69-821a1b0bc9e3` | What are the names and schools attended by politicians who have served as the head of state of a country to which the Ministry of National Defence belongs? |

Machine-readable labels, metrics, and predictions: `rebuttal/representative_50_first_two_columns_seed42.json` and `rebuttal/representative_50_first_two_columns_seed42.jsonl`.
