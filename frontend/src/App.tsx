import { useState, useEffect, useRef, useLayoutEffect } from "react";
import {
  Chart as ChartJS,
  RadialLinearScale,
  PointElement,
  LineElement,
  Filler,
  Tooltip,
  Legend,
} from "chart.js";
import { Radar } from "react-chartjs-2";
import "./App.scss";

ChartJS.register(
  RadialLinearScale,
  PointElement,
  LineElement,
  Filler,
  Tooltip,
  Legend
);

function App() {
  const [champsInfo, setChampsInfo] = useState<any>({});
  const [champ, setChamp] = useState<any>({
    name: "Aatrox",
    info: {
      attack: 8,
      defense: 4,
      magic: 3,
      difficulty: 4,
    },
    image: {
      full: "Aatrox.png",
      sprite: "champion0.png",
      group: "champion",
      x: 0,
      y: 0,
      w: 48,
      h: 48,
    },
  });

  const statsToParse = Object.entries(champ?.info) || [];
  const labelInfo =
    statsToParse?.map((stat) => {
      return stat[0];
    }) || [];
  const statDataInfo =
    statsToParse?.map((stat) => {
      return stat[1];
    }) || [];

  const data = {
    labels: labelInfo || [],
    datasets: [
      {
        label: `${champ.name} stats`,
        data: statDataInfo,
        backgroundColor: "rgba(255, 99, 132, 0.2)",
        borderColor: "rgba(255, 99, 132, 1)",
        borderWidth: 1,
      },
    ],
  };

  useEffect(() => {
    async function getChamps() {
      const res = await fetch(
        "https://ddragon.leagueoflegends.com/cdn/13.1.1/data/en_US/champion.json"
      );
      const parsedRes = await res.json();
      setChampsInfo(parsedRes.data as any);
    }
    getChamps();
    return () => {
      setChampsInfo([]);
    };
  }, []);

  return (
    <div className="App">
      <h1>LoL Sapiens</h1>

      {champsInfo && (
        <select
          onChange={(e) => {
            setChamp(champsInfo[e.target.value]);
          }}
        >
          {Object.keys(champsInfo).map((champ: any) => {
            return (
              <option value={champ} key={champ}>
                {champ}
              </option>
            );
          })}
        </select>
      )}

      <section className="Champion bg__gray">
        {champ.image && (
          <img
            src={`https://ddragon.leagueoflegends.com/cdn/13.1.1/img/champion/${
              champ.image?.full || ""
            }`}
          />
        )}

        <div className="Champion__info">
          <h2>{champ.name}</h2>
          <div className="Tags">
            {champ.tags.map((tag: string) => (
              <span className="Chip" key={tag}>
                {tag}
              </span>
            ))}
          </div>
        </div>
        <div className="Champion__stats">
          <Radar data={data} />
        </div>
      </section>
    </div>
  );
}

export default App;
