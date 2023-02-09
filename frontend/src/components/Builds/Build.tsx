import { useEffect, useState } from "react";
import path from "path";
import fs from "fs";
// import { remote } from "electron";
import "./build.scss";

interface BuildProps {
  champ: any;
  lane: string;
  tier: string;
  mode: string;
  spicy: string;
}

const Build = ({ champ, lane, tier, mode, spicy }: BuildProps) => {
  const [build, setBuild] = useState<any>(null);

  const getBuild = async () => {
    const res = await fetch(
      "http://localhost:3200/champion/build?" +
      new URLSearchParams({
        champion_id: champ?.key,
        lane,
        tier,
        mode,
        keystone_id: "8128",
        spicy,
      })
    );

    const parsedRes = await res.json();
    setBuild(parsedRes);
    console.log(parsedRes);
  };

  const importBuild = () => {
    console.log("Importing...");
    
    // const lolDirectory = path.dirname("C:/Riot Games/League of Legends");
    // const lolDirectory = path.join("/Users/sebasp/Documents/VSCode/LolSapiens/data");
    // const myFile = path.join(lolDirectory, "testing.txt");
    // console.log(myFile);

    // fs.writeFile(lolDirectory, "Un string!", (error) => {
    //   if (error) {
    //     console.log(error);
    //     return;
    //   }
    //   console.log(`File saved into ${myFile}`);
      
    // })
  }

  useEffect(() => {
    if (champ && tier && lane && mode && spicy) getBuild();
  }, [champ, tier, lane, mode, spicy]);

  return (
    build && (
      <section className="card bg__gray">
        <h2>{build.title}</h2>
        <button onClick={importBuild}>Import 🐶</button>
        <div className="build">
          {build.blocks && build.blocks.map((block: any) => (
            <div key={block.type} className="build-block">
              <p>{block.type}</p>
              <div className="build-block__items">
                {block.items.map((item: any, index: number) => (
                  // Se usa el index porque Sebastian manda items repetidos :/
                  <img
                    key={`${item.id}-${index}`}
                    src={`http://ddragon.leagueoflegends.com/cdn/13.1.1/img/item/${item.id}.png`}
                    alt={`item-${item.id}`}
                  />
                ))}
              </div>
            </div>
          ))}
          {!build.blocks && <h1>No build... 🗿</h1>}
        </div>
      </section>
    )
  );
};

export default Build;
