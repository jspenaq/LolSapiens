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

  // TODO:!! Arregle esto hpta, está mandando 3 peticiones al tiempo
  const getBuild = async (): Promise<void> => {
    try {
      const res = await fetch(
        // Construct the URL using query parameters
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

      // Parse the response and set the build state
      const parsedRes = await res.json();
      setBuild(parsedRes);
    } catch (error) {
      console.error("Error fetching build:", error);
    }
  };

  // Function to import the build into the desktop app (if running in Electron)
  const importBuild = (): void => {
    if (window.electronApi) {
      window.electronApi.importBuild({ championName: champ.id, build });
    } else {
      // Show an alert if not running in Electron
      alert(
        "Browser mode, If you want to import the build please use desktop app"
      );
    }
  };

  // Fetch the build data when any of the input parameters change
  useEffect(() => {
    if (champ && tier && lane && mode && spicy) getBuild();
  }, [champ, tier, lane, mode, spicy]);

  // Set up a listener for the buildImported event (if running in Electron)
  useEffect(() => {
    // No muy seguro de si es lo correcto en estos casos
    window.electronApi?.buildImported(() => {
      alert("Build imported successfully");
    });

    // Remove the listener when the component unmounts
    return () => {
      window.electronApi?.buildImported(() => { });
    };
  }, []);

  // Render the build data if it exists
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
                    src={`http://ddragon.leagueoflegends.com/cdn/13.1.1/img/item/${item.id as string
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
