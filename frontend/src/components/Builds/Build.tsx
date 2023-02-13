import { useEffect, useState } from "react";
import "./build.scss";

interface BuildProps {
  champ: any;
  lane: string;
  tier: string;
  mode: string;
  spicy: string;
}

const Build = ({ champ, lane, tier, mode, spicy }: BuildProps): JSX.Element => {
  const [build, setBuild] = useState<any>(null);

  // !! Arregle esto hpta, está mandando 3 peticiones al tiempo
  const getBuild = async (): Promise<void> => {
    const res = await fetch(
      // eslint-disable-next-line @typescript-eslint/restrict-plus-operands
      "http://localhost:3200/champion/build?" +
        new URLSearchParams({
          champion_id: champ?.key,
          lane,
          tier,
          mode,
          spicy,
        })
    );

    const parsedRes = await res.json();
    setBuild(parsedRes);
  };

  const importBuild = (): void => {
    if (window.electronApi) {
      window.electronApi.importBuild({ championName: champ.id, build });
    } else {
      alert(
        "Browser mode, If you want to import the build please use desktop app"
      );
    }
  };

  useEffect(() => {
    if (champ && tier && lane && mode && spicy) getBuild();
  }, [champ, tier, lane, mode, spicy]);

  useEffect(() => {
    // No muy seguro de si es lo correcto en estos casos
    window.electronApi?.buildImported(() => {
      alert("Build imported successfully");
    });

    return () => {
      window.electronApi?.buildImported(() => {});
    };
  }, []);

  return (
    build && (
      <section className="card bg__gray build">
        {build.blocks && (
          <hgroup className="build__title">
            <h2>{build.title}</h2>
            <button onClick={importBuild}>Import 🐶</button>
          </hgroup>
        )}

        <div className="build__result">
          {build.blocks?.map((block: any) => (
            <div key={block.type} className="build-block">
              <p>{block.type}</p>
              <div className="build-block__items">
                {block.items.map((item: any, index: number) => (
                  // Se usa el index porque Sebastian manda items repetidos :/
                  <img
                    key={`${item.id as string}-${index}`}
                    src={`http://ddragon.leagueoflegends.com/cdn/13.1.1/img/item/${
                      item.id as string
                    }.png`}
                    alt={`item-${item.id as string}`}
                  />
                ))}
              </div>
            </div>
          ))}
          {!build.blocks && (
            <p className="build__error">
              Your parameters seem to be too Spicy 🔥🔥🔥
            </p>
          )}
        </div>
      </section>
    )
  );
};

export default Build;
