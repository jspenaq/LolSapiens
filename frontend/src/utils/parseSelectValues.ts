export default function (stringToParse: string): string {
  const stringSections = stringToParse.split("_");
  return stringSections.reduce((acc, curr, index) => {
    return (
      acc + `${index > 0 ? " " : ""}` + curr[0].toUpperCase() + curr.slice(1)
    );
  }, "");
}
