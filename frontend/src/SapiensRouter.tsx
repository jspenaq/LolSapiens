import {
  createHashRouter,
  createRoutesFromElements,
  Route,
  useRouteError,
} from "react-router-dom";
import App from "./App";
import Picks from "./pages/Picks/Picks";

function ErrorBoundary(): JSX.Element {
  const error: any = useRouteError();
  console.error(error);
  return <div>{error.message}</div>;
}

const router = createHashRouter(
  createRoutesFromElements(
    <Route path="/" element={<App />} errorElement={<ErrorBoundary />}>
      {/* <Route index element={Gameflow element} /> */}
      <Route path="picks" element={<Picks />} />
      <Route path="search" element={<Picks />} />
    </Route>
  )
);

export default router;
