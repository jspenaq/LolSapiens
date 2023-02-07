import './select.scss'

type itemList = {
    id?: string,
    name?: string,
}

interface ISelectProps {
  itemList: itemList & Record<string, any>;
  onChangeCallback: Function;
  // Rest props
  [x: string]: any;
}

export default function Select({ itemList, onChangeCallback, ...props }: ISelectProps) {
  return (
    <select
      onChange={(e) => onChangeCallback(e.target.value)}
      // defaultValue="Aatrox"
      {...props}
      className="select"
    >
      {itemList.map(({ id, name }: any) => {
        return (
          <option value={id || name} key={id || name}>
            {name}
          </option>
        );
      })}
    </select>
  );
}
