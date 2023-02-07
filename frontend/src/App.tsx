import { useState, useEffect, Fragment } from "react";
import {
  Chart as ChartJS,
  RadialLinearScale,
  PointElement,
  LineElement,
  Filler,
  Tooltip as CharTooltip,
  Legend,
} from "chart.js";
import { Radar } from "react-chartjs-2";
import "./App.scss";
import Tooltip from "./Tooltip";

ChartJS.register(
  RadialLinearScale,
  PointElement,
  LineElement,
  Filler,
  CharTooltip,
  Legend
);

function App() {
  const [count, setCount] = useState(0);
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

  const getChampInfo = async (event: any) => {
    const champName = event.target.value;
    const res = await fetch(
      `http://ddragon.leagueoflegends.com/cdn/13.1.1/data/en_US/champion/${champName}.json`
    );
    const parsedRes = await res.json();
    setChamp(parsedRes.data[champName]);
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

  async function getChampName(name: string) {
    const res = await fetch(
      `https://ddragon.leagueoflegends.com/cdn/13.1.1/img/champion/${name}.png`
    );
  }

  console.log(champ);

  return (
    <div className="App">
      <h1>LoL Sapiens</h1>

      {champsInfo && (
        <select onChange={getChampInfo}>
          {Object.keys(champsInfo).map((champ: any) => {
            return (
              <option value={champ} key={champ}>
                {champ}
              </option>
            );
          })}
        </select>
      )}

      <section className="champion bg__gray">
        {champ.image && (
          <img
            src={`https://ddragon.leagueoflegends.com/cdn/13.1.1/img/champion/${
              champ.image?.full || ""
            }`}
          />
        )}

        <div className="champion__info">
          <h2>{champ.name}</h2>
          <span>{champ.title}</span>
          <div className="tags">
            {champ.tags &&
              champ.tags.map((tag: string) => (
                <span className="chip" key={tag}>
                  {tag}
                </span>
              ))}
          </div>
          <div className="spells">
            {champ.passive && (
              <img
                src={`https://ddragon.leagueoflegends.com/cdn/13.1.1/img/passive/${
                  champ.passive.image?.full || ""
                }`}
              />
            )}
            {champ.spells &&
              champ.spells.map((spell: any) => (
                <Fragment key={spell.id}>
                  <img
                    src={`https://ddragon.leagueoflegends.com/cdn/13.1.1/img/spell/${
                      spell.image?.full || ""
                    }`}
                  />
                  <Tooltip show={true}>{spell.description}</Tooltip>
                </Fragment>
              ))}
          </div>
        </div>
        <div className="champion__stats">
          <Radar data={data} />
        </div>
      </section>
    </div>
  );
}

export default App;
