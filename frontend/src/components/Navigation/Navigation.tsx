import { NavLink } from "react-router-dom";
import classes from "./navigation.module.scss";
import classNames from "classnames";

const Navigation = (): JSX.Element => {
  return (
    <header className={classes.navigation}>
      <h1>Summoner data</h1>
      <ul>
        <li>
          <NavLink
            to={"/"}
            className={({ isActive }) =>
              classNames({ [classes["link--active"]]: isActive })
            }
          >
            Gameflow
          </NavLink>
        </li>
        <li>
          <NavLink
            to={"/picks"}
            className={({ isActive }) =>
              classNames({ [classes["link--active"]]: isActive })
            }
          >
            Top 10 Bans & Picks
          </NavLink>
        </li>
        <li>
          <NavLink
            to={"/search"}
            className={({ isActive }) =>
              classNames({ [classes["link--active"]]: isActive })
            }
          >
            Search
          </NavLink>
        </li>
      </ul>
    </header>
  );
};

export default Navigation;
