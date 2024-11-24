---
sql:
  data_users: data/users.parquet
---

```sql id=data
SELECT *
FROM data_users
```

```js
const dataPlot = _.chain([...data])
    .map((d) => ({
      date: moment.utc(d["timestamp"]).toDate(),
      users: d.users
    }))
    .sortBy((d) => d.date)
    .value();

const chart = Plot.plot({
  marginRight:70,

  x:{type:"time", grid:true},
  y:{tickFormat: ".1s", grid:true},
  marks: [
    Plot.lineY(dataPlot, {
      x:"date", 
      y:"users", 
      tip:true,
      title:d => `${d3.format(",")(d.users)}\n${d.date}`
      }),
    Plot.text(dataPlot, Plot.selectLast({
      x:"date", 
      y:"users", 
      text:"users",
      textAnchor:"start",
      dx:5
      })),
  ]
})
```

<h1> Bluesky users </h2>
Last review at ${_.last([...dataPlot])["date"]}
<div class="card">
    ${chart}
</div>

<style>

.hero {
  display: flex;
  flex-direction: column;
  align-items: center;
  font-family: var(--sans-serif);
  margin: 4rem 0 8rem;
  text-wrap: balance;
  text-align: center;
}

.hero h1 {
  margin: 1rem 0;
  padding: 1rem 0;
  max-width: none;
  font-size: 14vw;
  font-weight: 900;
  line-height: 1;
  background: linear-gradient(30deg, var(--theme-foreground-focus), currentColor);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.hero h2 {
  margin: 0;
  max-width: 34em;
  font-size: 20px;
  font-style: initial;
  font-weight: 500;
  line-height: 1.5;
  color: var(--theme-foreground-muted);
}

@media (min-width: 640px) {
  .hero h1 {
    font-size: 90px;
  }
}

</style>

```js
import moment from 'npm:moment'
```
