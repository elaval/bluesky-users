---
sql:
  data_users: data/users.parquet
  archive_data: data/archive_data.json
---

```sql id=data
SELECT *
FROM data_users
```

```sql id=archive_data
SELECT *
FROM archive_data
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

## Bluesky Users: ${d3.format(",")(_.last([...dataPlot])["users"])}
Last update: ${_.last([...dataPlot])["date"]}
<div class="card">
    ${chartIntegrated}
    <div class="muted">
    <p></p>
Data Sources:
<ul>
<li>Current user counts sourced from a regularly updated time series maintained by @elaval.bsky.social since November 22, 2024, using an API by Theo Sanderson. <br> 
<li>Historical data derived from Web Archive snapshots of Jaz’s bsky stats.
</ul>
    </div>
</div>



```js
const dataPlotArchive = _.chain([...archive_data])
    .map((d) => ({
      date: moment.utc(d["date"]).toDate(),
      users: d.users
    }))
    .sortBy((d) => d.date)
    .filter(d => d.date >= new Date("2023-05-20"))
    .value();

const event_beta = dataPlotArchive.find((d) => d.date >= new Date("2023-02-01"));

const event_open = dataPlotArchive.find((d) => d.date >= new Date("2024-02-01"));

const event_elections = dataPlotArchive.find(
  (d) => d.date >= new Date("2024-11-05")
);

const event_x_blocked = dataPlotArchive.find(
  (d) => d.date >= new Date("2024-08-30")
);


const chartArchive = Plot.plot({
  marginRight:70,

  x:{type:"time", grid:true},
  y:{type:"log",tickFormat: ".1s", grid:true, label: "Total users (log scale)"},
  marks: [
      Plot.ruleY([1000000, 5000000, 10000000, 20000000], { strokeDasharray: "1" }),
      Plot.lineY(dataPlotArchive, {
        x: "date",
        y: "users",
        stroke: (d) => "bsky",
        strokeWidth: 5
      }),
      Plot.dot(dataPlotArchive, {
        x: "date",
        y: "users",
        r: 0.5,
        tip: true
      }),      Plot.text(dataPlotArchive, Plot.selectLast({
        x: "date",
        y: "users",
        text: "users"
      })),
      Plot.tip(
        [
          
 
          {
            date: event_elections["date"],
            users: event_elections["users"],
            text: "US elections"
          }
        ],
        { x: "date", y: "users", title: "text", anchor: "bottom-right" }
      ),
      Plot.tip(
        [         {
            date: event_open["date"],
            users: event_open["users"],
            text: "Open to public registration"
          },
          {
            date: event_x_blocked["date"],
            users: event_x_blocked["users"],
            text: "X blocked in Brazil"
          }
        ],
        { x: "date", y: "users", title: "text", anchor: "top-left" }
      )
  ]
})
```

```js
const dataPlotIntegrated = _.concat(dataPlotArchive, dataPlot)
  
const event_beta = dataPlotIntegrated.find((d) => d.date >= new Date("2023-02-01"));

const event_open = dataPlotIntegrated.find((d) => d.date >= new Date("2024-02-01"));

const event_elections = dataPlotIntegrated.find(
  (d) => d.date >= new Date("2024-11-05")
);

const event_x_blocked = dataPlotIntegrated.find(
  (d) => d.date >= new Date("2024-08-30")
);


const event_meta_factchecking = dataPlotIntegrated.find(
  (d) => d.date >= new Date("2025-01-07")
);



const chartIntegrated = Plot.plot({
  marginRight:70,
  marginTop:50,
  x:{type:"time", grid:true},
  y:{type:"linear",tickFormat: ".1s", grid:true, label: "Total users", domain:[0, 27000000]},
  marks: [
      Plot.ruleY([1000000, 5000000, 10000000, 20000000, 25000000], { strokeDasharray: "1" }),
      Plot.lineY(dataPlotIntegrated, {
        x: "date",
        y: "users",
        stroke: (d) => "bsky",
        strokeWidth: 5
      }),
      Plot.dot(dataPlotIntegrated, {
        x: "date",
        y: "users",
        r: 0.5,
        tip: true
      }),
       Plot.text(dataPlotIntegrated, Plot.selectLast({
        x: "date",
        y: "users",
        text: "users",
        textAnchor:"start", dx:5
      })),
      Plot.tip(
        [
          
 
          {
            date: event_elections["date"],
            users: event_elections["users"],
            text: "US elections"
          },
          {
            date: event_meta_factchecking["date"],
            users: event_meta_factchecking["users"],
            text: "Meta ends factchecking"
          }
        ],
        { x: "date", y: "users", title: "text", anchor: "bottom-right" }
      ),
      Plot.tip(
        [         {
            date: event_open["date"],
            users: event_open["users"],
            text: "Open to public registration"
          },
          {
            date: event_x_blocked["date"],
            users: event_x_blocked["users"],
            text: "X blocked in Brazil"
          }
        ],
        { x: "date", y: "users", title: "text", anchor: "top-left" }
      )
  ]
})
```



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
