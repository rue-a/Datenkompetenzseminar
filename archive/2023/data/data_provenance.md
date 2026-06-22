Monastery data was retrieved from [Wikidata](https://query.wikidata.org/) with the query:

```sparql
SELECT DISTINCT  ?monastery ?geometry ?foundingYear ?wikidata_entry WHERE {
  ?wikidata_entry wdt:P31/wdt:P279* wd:Q44613 .
  ?wikidata_entry wdt:P17 wd:Q183 .
  ?wikidata_entry wdt:P625 ?geometry .
  ?wikidata_entry wdt:P571 ?foundingDate .
  BIND(year(?foundingDate) AS ?foundingYear)  
  ?wikidata_entry rdfs:label ?monastery .
  FILTER(lang(?monastery) = "de" )
}
```

Brewery data was retrieved from [Wikidata](https://query.wikidata.org/) with the query:

```sparql
SELECT DISTINCT ?brewery ?geometry ?foundingYear ?wikidata_entry WHERE {
  ?wikidata_entry wdt:P31/wdt:P279* wd:Q131734 .
  ?wikidata_entry wdt:P17 wd:Q183 .
  {
    ?wikidata_entry wdt:P625 ?geometry .
  } 
  OPTIONAL {
    ?wikidata_entry wdt:P159 ?headquarters .
    ?headquarters wdt:P625 ?geometry .
  } OPTIONAL {
    ?wikidata_entry wdt:P131 ?adminEntity .
    ?adminEntity wdt:P625 ?geomerty .
  }
  OPTIONAL {
    ?wikidata_entry wdt:P571 ?foundingDate .
    BIND(year(?foundingDate) AS ?foundingYear)
  }
  ?wikidata_entry rdfs:label ?brewery .
  FILTER(lang(?brewery) = "de")
}
```

Monastery data by religious order was retrieved with the following queries:

- Zisterzienser

```sparql
SELECT DISTINCT  ?monastery ?geometry ?year ?wikidata_entry WHERE {
  ?wikidata_entry wdt:P31/wdt:P279* wd:Q44613 .
  ?wikidata_entry wdt:P17 wd:Q183 .
  ?wikidata_entry wdt:P625 ?geometry .
  ?wikidata_entry rdfs:label ?monastery .
  ?wikidata_entry wdt:P571 ?foundingDate .
  BIND(year(?foundingDate) AS ?year)  
  ?wikidata_entry rdfs:label ?monastery .
  FILTER(lang(?monastery) = "de" )
  FILTER(CONTAINS(LCASE(?monastery), "zisterzienser"))
}
```

- Benediktiner

```sparql
SELECT DISTINCT  ?monastery ?geometry ?year ?wikidata_entry WHERE {
  ?wikidata_entry wdt:P31/wdt:P279* wd:Q44613 .
  ?wikidata_entry wdt:P17 wd:Q183 .
  ?wikidata_entry wdt:P625 ?geometry .
  ?wikidata_entry rdfs:label ?monastery .
  ?wikidata_entry wdt:P571 ?foundingDate .
  BIND(year(?foundingDate) AS ?year)  
  ?wikidata_entry rdfs:label ?monastery .
  FILTER(lang(?monastery) = "de" )
  FILTER(CONTAINS(LCASE(?monastery), "benediktiner"))
}
```

- Augustiner

```sparql
SELECT DISTINCT  ?monastery ?geometry ?year ?wikidata_entry WHERE {
  ?wikidata_entry wdt:P31/wdt:P279* wd:Q44613 .
  ?wikidata_entry wdt:P17 wd:Q183 .
  ?wikidata_entry wdt:P625 ?geometry .
  ?wikidata_entry rdfs:label ?monastery .
  ?wikidata_entry wdt:P571 ?foundingDate .
  BIND(year(?foundingDate) AS ?year)  
  ?wikidata_entry rdfs:label ?monastery .
  FILTER(lang(?monastery) = "de" )
  FILTER(CONTAINS(LCASE(?monastery), "augustiner"))
}
```

- Jesuiten

```sparql
SELECT DISTINCT  ?monastery ?geometry ?year ?wikidata_entry WHERE {
  ?wikidata_entry wdt:P31/wdt:P279* wd:Q44613 .
  ?wikidata_entry wdt:P17 wd:Q183 .
  ?wikidata_entry wdt:P625 ?geometry .
  ?wikidata_entry rdfs:label ?monastery .
  ?wikidata_entry wdt:P571 ?foundingDate .
  BIND(year(?foundingDate) AS ?year)  
  ?wikidata_entry rdfs:label ?monastery .
  FILTER(lang(?monastery) = "de" )
  FILTER(CONTAINS(LCASE(?monastery), "jesuiten"))
}
```

- Dominikaner

```sparql
SELECT DISTINCT  ?monastery ?geometry ?year ?wikidata_entry WHERE {
  ?wikidata_entry wdt:P31/wdt:P279* wd:Q44613 .
  ?wikidata_entry wdt:P17 wd:Q183 .
  ?wikidata_entry wdt:P625 ?geometry .
  ?wikidata_entry rdfs:label ?monastery .
  ?wikidata_entry wdt:P571 ?foundingDate .
  BIND(year(?foundingDate) AS ?year)  
  ?wikidata_entry rdfs:label ?monastery .
  FILTER(lang(?monastery) = "de" )
  FILTER(CONTAINS(LCASE(?monastery), "dominikaner"))
}
```

- Johanniter

```sparql
SELECT DISTINCT  ?monastery ?geometry ?year ?wikidata_entry WHERE {
  ?wikidata_entry wdt:P31/wdt:P279* wd:Q44613 .
  ?wikidata_entry wdt:P17 wd:Q183 .
  ?wikidata_entry wdt:P625 ?geometry .
  ?wikidata_entry rdfs:label ?monastery .
  ?wikidata_entry wdt:P571 ?foundingDate .
  BIND(year(?foundingDate) AS ?year)  
  ?wikidata_entry rdfs:label ?monastery .
  FILTER(lang(?monastery) = "de" )
  FILTER(CONTAINS(LCASE(?monastery), "johanniter"))
}
```