import { ChampionBuild } from "../../components";
import classes from "./search.module.scss";

const Search = (): JSX.Element => {
  return (
    <section className={classes.search}>
      <ChampionBuild />
    </section>
  );
};
export default Search;
