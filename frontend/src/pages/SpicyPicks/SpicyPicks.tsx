import { BanList, Select } from "../../components";
import useSpicyPicks from "../../hooks/useSpicyPicks";
import classes from "./spicypicks.module.scss";
import { lanes, tiers } from "../../constants";
import { useState } from "react";
import type { Option } from "../../types";

const SpicyPicks = (): JSX.Element => {
  const [tier, setTier] = useState<Option | null>(tiers[0]);
  const [lane, setLane] = useState<Option | null>(lanes[0]);

  const { data: bans } = useSpicyPicks({
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
    <section className={classes["spicy-picks"]}>
      <h1>Top 10</h1>
      <div className={classes.controls}>
        <Select options={tiers} onChange={handleTier} defaultValue={tier} />
        <Select options={lanes} onChange={handleLane} defaultValue={lane} />
      </div>

      {bans && Boolean(bans.length) && <BanList bans={bans} />}
    </section>
  );
};

export default SpicyPicks;
