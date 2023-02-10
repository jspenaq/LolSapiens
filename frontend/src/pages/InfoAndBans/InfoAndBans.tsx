import { useState, useEffect } from "react";
import championsData from "../../../../data/champions_data.json";
import { lanes, tiers, modes, spicyList } from "../../constants";
import { ChampionCard, Bans, Select, Build } from "../../components";

const championList = championsData
  ? Object.values(championsData).sort((a: any, b: any) => {
      return a.name.localeCompare(b.name);
    })
  : [];

function InfoAndBans() {
  const [lane, setLane] = useState("default");
  const [tier, setTier] = useState("gold_plus");
  const [mode, setMode] = useState("ranked");
  const [spicy, setSpicy] = useState("0");
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
      <section className="card bg__gray selects">
        <Select
          itemList={championList}
          onChangeCallback={getChampInfo}
          defaultValue={champ?.name || "Aatrox"}
        />
        <Select
          itemList={lanes}
          onChangeCallback={setLane}
          defaultValue={lanes.find((el) => el.id === lane)?.name}
        />
        <Select
          itemList={tiers}
          onChangeCallback={setTier}
          defaultValue={tiers.find((el) => el.id === tier)?.name}
        />
        <Select
          itemList={modes}
          onChangeCallback={setMode}
          defaultValue={modes.find((el) => el.id === mode)?.name}
        />
        <Select
          itemList={spicyList}
          onChangeCallback={setSpicy}
          defaultValue={spicyList.find((el) => el.id === spicy)?.name}
        />
      </section>
      {mode === "ranked" && (
        <Bans lane={lane} tier={tier} champ={champ} champsInfo={champsInfo} />
      )}
      <ChampionCard champion={champ} />
      <Build lane={lane} tier={tier} mode={mode} spicy={spicy} champ={champ} />
    </div>
  );
}

export default InfoAndBans;
