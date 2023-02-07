import { useState, useEffect } from "react";
import { parseSelectValues } from "../../utils";
import Tooltip from "../Tooltip";
import "./bans.scss";

export default function Bans({ champ, lane, tier, champsInfo }: any) {
  const [topBans, setTopBans] = useState([]);
  const getTopBans = async () => {
    const res = await fetch(
      `http://localhost:3200/bans/top10?` +
        new URLSearchParams({
          lane,
          tier,
        })
    );
    const parsedRes = await res.json();
    setTopBans(parsedRes);
  };

  useEffect(() => {
    if (lane && tier) {
      getTopBans();
    }
  }, [lane, tier]);

  return (
    <section className="card bg__gray">
      <h2>
        Top 10 Bans Lane: {parseSelectValues(lane)}, Tier:{" "}
        {parseSelectValues(tier)}
      </h2>
      <div className="topBans">
        {Boolean(topBans.length) &&
          topBans.map((champion: any) => {
            const { id, name, value, win_rate, pick_rate } = champion;
            const imgPath = champsInfo[value].image.full;
            return (
              <div key={id} className="topBans__champion">
                <Tooltip text={name}>
                  <img
                    height={54}
                    src={`https://ddragon.leagueoflegends.com/cdn/13.1.1/img/champion/${
                      imgPath || ""
                    }`}
                  />
                </Tooltip>
                <div className="ban-description">
                  <p>{name}</p>
                  <p className="ban-description__wr">
                    WR: {win_rate.toFixed(2)}%
                  </p>
                  <p className="ban-description__pr">
                    PR: {pick_rate.toFixed(2)}%
                  </p>
                </div>
              </div>
            );
          })}
      </div>
    </section>
  );
}
