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
    .slice(-24*5)
    .value();

const chart = Plot.plot({
  marginRight:70,
  caption:"Chart author: @elaval.bsky.social",
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

## Bluesky Users Since Nov 22, 2024
Last update: ${_.last([...dataPlot])["date"]}  
Last report: **${d3.format(",")(_.last([...dataPlot])["users"])} users** 
<div class="card">
    ${chart}
</div>

### Data Sources and Updates
The data presented on this webpage is compiled and updated regularly (approximately every hour) from the following sources and tools:
* Primary Data Compilation:
The total user count is updated regularly since Nov 22, 2024, by [elaval.bsky.social](https://bsky.app/profile/elaval.bsky.social) using GitHub Actions. The data is fetched via an API created by Theo Sanderson.  
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
