import { useState } from "react";
import { lanes, tiers } from "../../constants";
import useTop10 from "../../hooks/useTop10";
import type { Option } from "../../types";
import ChampionList from "../BanList/ChampionList";
import Select from "../Select/Select";
import classes from "./banphase.module.scss";

const BanPhase = (): JSX.Element => {
  const [tier, setTier] = useState<Option | null>(tiers[0]);
  const [lane, setLane] = useState<Option | null>(lanes[0]);

  const { data: bans } = useTop10({
    lane: lane?.value ?? "default",
    tier: tier?.value ?? "gold_plus",
  });

  const handleTier = (newValue: Option | null): void => {
    setTier(newValue);
  };
  const handleLane = (newValue: Option | null): void => {
    setLane(newValue);
  };

  return (
    <>
      <div className={classes.controls}>
        <Select options={tiers} onChange={handleTier} defaultValue={tier} />
        <Select options={lanes} onChange={handleLane} defaultValue={lane} />
      </div>

      {bans && Boolean(bans.length) && <ChampionList champions={bans} areBan />}
    </>
  );
};

export default BanPhase;
