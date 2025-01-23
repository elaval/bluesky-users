---
sql:
  data_users: data/users.parquet
  archive_data: data/archive_data.json
---
```js
function isFirefox() {
    return navigator.userAgent.includes("Firefox");
}
```
${isFirefox() ? html`<div style="background-color:yellow">Nota: Se han reportado errores al usar <b>Firefox</b>.  Si la página arroja errores, por favor intentar con otro navegador </div>`: ``}


```sql id=data
SELECT *
FROM data_users
```

```sql id=archive_data
SELECT *
FROM archive_data
```

```js

let prev = null;
const tasa = []
const analysis = _.chain([...data])
.each(d => {
  if (prev) {
    const diffSeconds = moment(d.timestamp).diff(moment(prev.timestamp), "seconds")
    const diffUsers = d.users - prev.users
    tasa.push({
      timestamp: d.timestamp,
      diffTime: diffSeconds,
      diffUsers:diffUsers,
      tasa: diffUsers / diffSeconds
    })
  }
  prev = d;
})
.value()
```

```js

let prev = null;
const tasa24h = []
const analysis24h = _.chain([...data])
.each((d,i) => {
  if (prev) {
    const diffHours = moment(d.timestamp).diff(moment(prev.timestamp), "hours")
    const diffUsers = d.users - prev.users
    tasa24h.push({
      timestamp: d.timestamp,
      diffTime: diffHours,
      diffUsers:diffUsers,
      tasa: 24 * diffUsers / diffHours
    })
  }
  prev = i >=24 ? [...data][i-24] : null;
  //display([i,prev])
})
.value()
```

```js
const dataPlot = _.chain([...data])
    .map((d) => ({
      date: moment.utc(d["timestamp"]).toDate(),
      users: d.users
    }))
    .sortBy((d) => d.date)
    .slice(-24*14)
    .value();

const chart = Plot.plot({
  marginLeft:70,
  marginRight:70,
  title: "Total number of Bluesky users",

  caption:"Chart author: (@elaval.bsky.social)[https://bsky.app/profile/elaval.bsky.social]",
  x:{type:"time", grid:true},
  y:{tickFormat: ".1s", grid:true, type:"linear"},
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


```js
const dataPlotTasa = _.chain(tasa)
    .map((d) => ({
      date: moment.utc(d["timestamp"]).toDate(),
      tasa: d.tasa
    }))
    .sortBy((d) => d.date)
    .slice(-24*14)
    .value();

const chartTasa = Plot.plot({
  marginLeft:70,
  marginRight:70,
  title: "Rate of new Bluesky users per second",
  caption:"Chart author: @elaval.bsky.social",
  x:{type:"time", grid:true},
  y:{tickFormat: ".1s", grid:true, type:"linear", label:"Rate of new users per second"},
  marks: [
    Plot.lineY(dataPlotTasa, {
      x:"date", 
      y:"tasa", 
      tip:true,
      title:d => `${d3.format(",")(d.tasa)}\n${d.date}`
      }),
    Plot.text(dataPlotTasa, Plot.selectLast({
      x:"date", 
      y:"users", 
      text:"users",
      textAnchor:"start",
      dx:5
      })),
  ]
})
```

## Bluesky Users Since ${moment(dataPlot[0].date).format("DD MMM YYYY")}
Last update: ${_.last([...dataPlot])["date"]}  
Last report: **${d3.format(",")(_.last([...dataPlot])["users"])} users** 
<div class="card">
    ${chart}
</div>

<div class="card">
    ${chartTasa}
</div>


```js
const dataPlotTasa24h = _.chain(tasa24h)
    .map((d) => ({
      date: moment.utc(d["timestamp"]).toDate(),
      tasa: d.tasa
    }))
    .sortBy((d) => d.date)
    .slice(-24*17)
    .value();

const chartTasa24h = Plot.plot({
  marginLeft:70,
  marginRight:70,
  title: "Rate of new Bluesky users in 24 hours",
  caption:"Chart author: @elaval.bsky.social",
  x:{type:"time", grid:true},
  y:{tickFormat: ".1s", grid:true, type:"linear", label:"Rate of new users per 24h"},
  marks: [
    Plot.lineY(dataPlotTasa24h, {
      x:"date", 
      y:"tasa", 
      tip:true,
      title:d => `${d3.format(",")(d.tasa)}\n${d.date}`
      }),
    Plot.text(dataPlotTasa24h, Plot.selectLast({
      x:"date", 
      y:"users", 
      text:"users",
      textAnchor:"start",
      dx:5
      })),
  ]
})
```

<div class="card">
    ${chartTasa24h}
</div>

### Data Sources and Updates
The data presented on this webpage is compiled and updated regularly (approximately every hour) from the following sources and tools:
* Primary Data Compilation:
The total user count is updated regularly since ${moment(dataPlot[0].date).format("DD MMM YYYY")}, by [elaval.bsky.social](https://bsky.app/profile/elaval.bsky.social) using GitHub Actions. The data is fetched via an API created by Theo Sanderson.  
The compiled dataset is publicly accessible as a CSV file at: https://raw.githubusercontent.com/elaval/bskyusers/refs/heads/main/bsky_users_history.csv.
* API Data Source:
The data is retrieved from the stats API created by [Theo Sanderson](https://bsky.app/profile/theo.io): https://bsky-users.theo.io/api/stats.
* Underlying Data:
Theo Sanderson's stats API is powered by [Jaz's bsky stats](https://bsky.jazco.dev/stats).


<style>


@media (min-width: 640px) {
  .hero h1 {
    font-size: 90px;
  }
}

</style>

```js
import moment from 'npm:moment'
```
