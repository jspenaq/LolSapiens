import { BanPhase, ChampionBuild, Loading } from "../../components";
import { useAppSelector } from "../../hooks/reduxHooks";
import classes from "./gameflow.module.scss";

const Gameflow = (): JSX.Element => {
  const gameflow = useAppSelector((state) => state.leagueClient.gameflow);
  const champion = useAppSelector(
    (state) => state.leagueClient.currentChampion
  );

  return (
    <section className={classes.gameflow}>
      <h2>{gameflow?.gamePhase}</h2>
      <h3>{gameflow?.gameMode}</h3>

      {gameflow?.gamePhase !== "ChampSelect" && !champion && (
        <Loading text="Currently, you aren't in Champion Selection phase. Waiting... " />
      )}

      {gameflow?.gamePhase === "ChampSelect" && !champion && (
        <div className={classes.bans}>
          <p>Pick/Bans recommendations</p>
          <BanPhase />
        </div>
      )}

      {champion && (
        <ChampionBuild
          initialQuery={{
            champion_id: champion,
            keystone_id: "0",
            mode: gameflow?.gameMode,
            lane: "default",
          }}
          hideGameflowSelects
        />
      )}
    </section>
  );
};

export default Gameflow;
