import classes from "./picks.module.scss";

export default function Picks(): JSX.Element {
  const fakeChamps = new Array(10).fill("");

  return (
    <section className={classes.picks}>
      <h1>SpicyPicks</h1>

      <div className={classes.champions}>
        {fakeChamps.map((_, index) => {
          return (
            <article key={index}>
              <img
                src="http://ddragon.leagueoflegends.com/cdn/img/champion/loading/Aatrox_0.jpg"
                alt="algo"
              />
            </article>
          );
        })}
      </div>
    </section>
  );
}
