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
  const [lane, setLane] = useState("default");
  const [tier, setTier] = useState("gold_plus");
  const [topBans, setTopBans] = useState([]);
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

  const getTopBans = async () => {
    const res = await fetch(
      `http://localhost:3200/bans/top10?` +
        new URLSearchParams({
          lane,
          tier,
        })
    );
    const parsedRes = await res.json();
    setTopBans(Object.values(parsedRes));
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

  useEffect(() => {
    if (champ && lane && tier) {
      getTopBans();
    }
  }, [champ, lane, tier]);

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

      <select onChange={(e) => setLane(e.target.value)} defaultValue={lane}>
        <option value="default">default</option>
        <option value="top">top</option>
        <option value="jungle">jungle</option>
        <option value="middle">middle</option>
        <option value="bottom">bottom</option>
        <option value="support">support</option>
      </select>

      <select onChange={(e) => setTier(e.target.value)} defaultValue={tier}>
        <option value="1trick">1trick</option>
        <option value="diamond_plus">diamond_plus</option>
        <option value="platinum_plus">platinum_plus</option>
        <option value="gold_plus">gold_plus</option>
        <option value="platinum">platinum</option>
        <option value="gold">gold</option>
        <option value="silver">silver</option>
      </select>

      <section className="card champion bg__gray">
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
              <Tooltip text={champ.passive.description}>
                <img
                  height={48}
                  src={`https://ddragon.leagueoflegends.com/cdn/13.1.1/img/passive/${
                    champ.passive.image?.full || ""
                  }`}
                />
              </Tooltip>
            )}
            {champ.spells &&
              champ.spells.map((spell: any) => (
                <Tooltip key={spell.id} text={spell.description}>
                  <img
                    height={48}
                    src={`https://ddragon.leagueoflegends.com/cdn/13.1.1/img/spell/${
                      spell.image?.full || ""
                    }`}
                  />
                </Tooltip>
              ))}
          </div>
        </div>
        <div className="champion__stats">
          <Radar data={data} />
        </div>
      </section>
      <section className="card  bg__gray">
        <h4>
          Top 10 Bans Lane: {lane}, Tier: {tier}
        </h4>
        <div className="topBans">
          {Boolean(topBans.length) &&
            topBans.map((champName) => {
              const imgPath = champsInfo[champName].image.full;
              return (
                <div className="topBans__champion">
                  <Tooltip text={champName}>
                    <img
                      key={champName}
                      height={54}
                      src={`https://ddragon.leagueoflegends.com/cdn/13.1.1/img/champion/${
                        imgPath || ""
                      }`}
                    />
                  </Tooltip>
                  <span>{champName}</span>
                </div>
              );
            })}
        </div>
      </section>
    </div>
  );
}

export default App;
