import "./summoner.scss";

const Summoner = ({ summoner }: { summoner: any }): JSX.Element => {
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
