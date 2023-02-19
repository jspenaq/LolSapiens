import classes from "./loading.module.scss";
import LolSapiensLogo from "../../assets/images/logo.png";

interface LoadingProps {
  text?: string;
}

const Loading = ({ text }: LoadingProps): JSX.Element => {
  return (
    <div className={classes.loading}>
      <img src={LolSapiensLogo} alt="LolSapiensLogo jalapeno" />
      {text && <span>{text}</span>}
    </div>
  );
};

export default Loading;
