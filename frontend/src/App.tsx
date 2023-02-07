import { useState, useEffect, Fragment } from "react";
import "./App.scss";
import championsData from "../../data/champions_data.json";
import ChampionCard from "./components/ChampionCard/ChampionCard";
import { lanes, tiers } from './constants';
import Select from "./components/Select/Select";
import Bans from "./components/Bans/Bans";

const championList = championsData
  ? Object.values(championsData).sort((a: any, b: any) => {
      return a.name.localeCompare(b.name);
    })
  : [];


function App() {
  const [lane, setLane] = useState("default");
  const [tier, setTier] = useState("gold_plus");
  const [champsInfo, setChampsInfo] = useState<any>({});
  const [champ, setChamp] = useState<any>(null);

  const getChampInfo = async (champName: string) => {
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

  if (champsInfo && !champ) {
    getChampInfo("Aatrox");
  }

  return (
    <div className="App">
      <h1>LoL Sapiens</h1>
      <section className="card bg__gray selects">
        <Select
          itemList={championList}
          onChangeCallback={getChampInfo}
          defaultValue={"Aatrox"}
        />
        <Select
          itemList={lanes}
          onChangeCallback={setLane}
          defaultValue={tier}
        />
        <Select
          itemList={tiers}
          onChangeCallback={setTier}
          defaultValue={tier}
        />
      </section>
      <ChampionCard champion={champ} />
      <Bans lane={lane} tier={tier} champ={champ} champsInfo={champsInfo}/>
    </div>
  );
}

export default App;
