import type { Build } from "../../types";
import classes from "./recommendedbuild.module.scss";
import { DDRAGON_BASE, DDRAGON_ITEM } from "../../constants/endpoints";
import { useAppSelector } from "../../hooks/reduxHooks";

export interface RecommendedBuildProps {
  build: Build;
}

const RecommendedBuild = ({ build }: RecommendedBuildProps): JSX.Element => {
  const patch = useAppSelector((state) => state.leagueApi.patch);

  return (
    <div className={classes.build}>
      <h3>Recommended Build</h3>
      <ul>
        {build.blocks?.map((block, index) => (
          <li key={`${index}-${block.type}`}>
            <p>{block.type}</p>
            <ul className={classes.block__items}>
              {block.items.map((item, index) => (
                <li key={`${index}-${item.id}`}>
                  <img
                    src={`${DDRAGON_BASE}/cdn/${patch}${DDRAGON_ITEM}/${item.id}.png`}
                    alt={`Item ${item.id} `}
                  />
                </li>
              ))}
            </ul>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default RecommendedBuild;
