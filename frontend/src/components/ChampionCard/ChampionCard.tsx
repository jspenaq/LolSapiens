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
import Tooltip from "../Tooltip";
import "./championCard.scss";

ChartJS.register(
  RadialLinearScale,
  PointElement,
  LineElement,
  Filler,
  CharTooltip,
  Legend
);

export default function ChampionCard({
  champion,
}: {
  champion: any;
}): JSX.Element {
  const statsToParse = champion ? Object.entries(champion?.info) : [];
  const labelInfo = statsToParse?.map((stat) => {
    return stat[0];
  });
  const statDataInfo = statsToParse?.map((stat) => {
    return stat[1];
  });

  const data = {
    labels: labelInfo || [],
    datasets: [
      {
        label: `${champion?.name} stats`,
        data: statDataInfo,
        backgroundColor: "rgba(255, 99, 132, 0.2)",
        borderColor: "rgba(255, 99, 132, 1)",
        borderWidth: 1,
      },
    ],
  };

  return (
    <section className="card champion bg__gray">
      {champion?.image && (
        <img
          src={`https://ddragon.leagueoflegends.com/cdn/13.1.1/img/champion/${
            champion.image?.full || ""
          }`}
        />
      )}

      <div className="champion__info">
        <h2>{champion?.name}</h2>
        <span>{champion?.title}</span>
        <div className="tags">
          {champion?.tags &&
            champion.tags.map((tag: string) => (
              <span className="chip" key={tag}>
                {tag}
              </span>
            ))}
        </div>
        <div className="spells">
          {champion?.passive && (
            <Tooltip text={champion.passive.description}>
              <img
                height={48}
                src={`https://ddragon.leagueoflegends.com/cdn/13.1.1/img/passive/${
                  champion.passive.image?.full || ""
                }`}
              />
            </Tooltip>
          )}
          {champion?.spells &&
            champion.spells.map((spell: any) => (
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
  );
}
