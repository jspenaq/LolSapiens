import { useEffect, useState } from "react";
import "./summoner.scss";

const Summoner = (): JSX.Element => {
  const [summoner, setSummoner] = useState<any>(null);

  useEffect(() => {
    window.electronApi?.summonerDetected((event: any, summoner: any) => {
      setSummoner(summoner);
    });
    return () => {
      window.electronApi?.summonerDetected(() => {});
    };
  }, []);

  if (!summoner) return <></>;

  return (
    <div className="summoner">
      <img
        src={`http://ddragon.leagueoflegends.com/cdn/13.3.1/img/profileicon/${
          summoner.profileIconId as string
        }.png`}
        alt={summoner.profileIconId}
      />
      <h2>{summoner.displayName}</h2>
      <progress max="100" value={summoner.percentCompleteForNextLevel}>
        {summoner.percentCompleteForNextLevel}
      </progress>
      <span>{summoner.summonerLevel}</span>
    </div>
  );
};
export default Summoner;
