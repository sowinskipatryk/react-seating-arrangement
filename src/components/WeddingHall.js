import { useDispatch } from "react-redux";
import { tablesActions } from "../store/tablesSlice";
import TableContainer from "./TableContainer";
import HorizontalContainer from "./UI/HorizontalContainer";

const TABLE_SIZES = [6, 20, 16, 16, 20, 20];

const sumValuesUntilIndex = (arr, index) => {
  let sum = 0;
  for (let i = 0; i < index; i++) {
    sum += arr[i];
  }
  return sum;
};

const WeddingHall = () => {
  const socket = new WebSocket('ws://localhost:8000/calculate/');
  const dispatch = useDispatch();

socket.onopen = () => {
  console.log('WebSocket connection established.');
};

socket.onmessage = (event) => {
  const result = JSON.parse(event.data);
  dispatch(tablesActions.setGuests(result.guests));
  dispatch(tablesActions.setProbabilities(result.probabilities));
};
  const handleClick = () => {
    socket.send('start calculation');
  };

  return (
    <div style={{position: 'relative'}}>
      <div style={{position: 'absolute'}}>
        <TableContainer
          startPosition={sumValuesUntilIndex(TABLE_SIZES, 0)}
          up="6"
          down="0"
          left="0"
          right="0"
          width="360px"
          height="100px"
          tableStyle={{ transform: "translate(330px, -40px)" }}
        />
      </div>
        <HorizontalContainer>
          <TableContainer
            startPosition={sumValuesUntilIndex(TABLE_SIZES, 1)}
            up="0"
            down="0"
            left="10"
            right="10"
            width="100px"
            height="550px"
          />
          <TableContainer
            startPosition={sumValuesUntilIndex(TABLE_SIZES, 2)}
            up="0"
            down="0"
            left="8"
            right="8"
            width="100px"
            height="500px"
            seatLeftStyle={{ paddingTop: "103px" }}
            seatRightStyle={{ paddingTop: "103px" }}
          />
          <TableContainer
            startPosition={sumValuesUntilIndex(TABLE_SIZES, 3)}
            up="0"
            down="0"
            left="8"
            right="8"
            width="100px"
            height="500px"
            seatLeftStyle={{ paddingTop: "103px" }}
            seatRightStyle={{ paddingTop: "103px" }}
          />
          <TableContainer
            startPosition={sumValuesUntilIndex(TABLE_SIZES, 4)}
            up="0"
            down="0"
            left="10"
            right="10"
            width="100px"
            height="550px"
          />
          <TableContainer
            startPosition={sumValuesUntilIndex(TABLE_SIZES, 5)}
            up="0"
            down="0"
            left="10"
            right="10"
            width="100px"
            height="550px"
          />
        </HorizontalContainer>
        <button onClick={handleClick}>Click me</button>
    </div>
  );
};

export default WeddingHall;
