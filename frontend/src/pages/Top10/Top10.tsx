import { BanList } from "../../components";
import useTop10 from "../../hooks/useTop10";
import classes from "./top10.module.scss";

const Top10 = (): JSX.Element => {
  const { data: bans } = useTop10({ lane: "middle", tier: "gold" });

  return (
    <section className={classes.top10}>
      <h1>Top 10</h1>

      {bans && Boolean(bans.length) && <BanList bans={bans} />}
    </section>
  );
};

export default Top10;
