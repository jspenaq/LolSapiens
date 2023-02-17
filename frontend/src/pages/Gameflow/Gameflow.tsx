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

      {gameflow?.gameMode !== "ChampSelect" && !champion && <p>Waiting...</p>}

      {gameflow?.gamePhase === "ChampSelect" && !champion && (
        <p>Here will be the Bans/ Picks</p>
      )}

      {champion && <p>Here will be the champion build/runes recommendation</p>}
    </section>
  );
};

export default Gameflow;
