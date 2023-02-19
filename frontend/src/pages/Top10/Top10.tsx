import { BanPhase } from "../../components";
import classes from "./top10.module.scss";

const Top10 = (): JSX.Element => {
  return (
    <section className={classes.top10}>
      <h1>Top 10</h1>
      <BanPhase />
    </section>
  );
};

export default Top10;
