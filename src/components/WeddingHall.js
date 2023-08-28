import { useDispatch, useSelector } from "react-redux";
import { useState, useEffect } from "react";
import { tablesActions } from "../store/tablesSlice";
import TableContainer from "./TableContainer";
import HorizontalContainer from "./UI/HorizontalContainer";

const sumValuesUntilIndex = (arr, index) => {
  let sum = 0;
  for (let i = 0; i < index; i++) {
    sum += arr[i];
  }
  return sum;
};

const socket = new WebSocket('ws://localhost:8000/');

const WeddingHall = () => {
  const dispatch = useDispatch();
  const [scaleFactor, setScaleFactor] = useState(1);
  const tableSizes = useSelector(state => state.tables.tableSizes);
  const score = useSelector(state => state.tables.score);
  const iteration = useSelector(state => state.tables.iteration);
  const [isRunning, setIsRunning] = useState(false);

  socket.onopen = () => {
    console.log('WebSocket connection established.');
  };
  
  socket.onmessage = (event) => {
      const result = JSON.parse(event.data);
      if (!result.isRunning) {
        setIsRunning(false);
      } else {
      dispatch(tablesActions.setArrangement(result.arrangement));
      dispatch(tablesActions.setSeatCosts(result.seatCosts));
      dispatch(tablesActions.setScore(result.score));
      dispatch(tablesActions.setIteration(result.iteration));
      }
  };

  socket.onerror = (error) => {
    console.error('WebSocket error:', error);
  };

  useEffect(() => {
    const handleResize = () => {
      const newScaleFactor = window.innerHeight / 930;
      setScaleFactor(newScaleFactor);
    };

    // Initial setup
    handleResize();

    // Attach the event listener
    window.addEventListener('resize', handleResize);

    // Clean up the event listener on component unmount
    return () => {
      window.removeEventListener('resize', handleResize);
    };
  }, []);

  const handleClick = () => {
    if (!isRunning) {
      setIsRunning(true);
      socket.send('start');
    } else {
      setIsRunning(false);
      socket.send('stop');
    }
  };

  return (
    <div className="simmulator" style={{ position: 'relative', transform: `scale(${scaleFactor})` }}>
      <div style={{position: 'absolute'}}>
        <TableContainer
          startPosition={sumValuesUntilIndex(tableSizes, 0)}
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
            startPosition={sumValuesUntilIndex(tableSizes, 1)}
            up="0"
            down="0"
            left="10"
            right="10"
            width="100px"
            height="550px"
            seatLeftStyle={{ flexDirection: 'column-reverse' }}
          />
          <TableContainer
            startPosition={sumValuesUntilIndex(tableSizes, 2)}
            up="0"
            down="0"
            left="8"
            right="8"
            width="100px"
            height="500px"
            seatLeftStyle={{ paddingTop: "103px", flexDirection: 'column-reverse' }}
            seatRightStyle={{ paddingTop: "103px" }}
          />
          <TableContainer
            startPosition={sumValuesUntilIndex(tableSizes, 3)}
            up="0"
            down="0"
            left="8"
            right="8"
            width="100px"
            height="500px"
            seatLeftStyle={{ paddingTop: "103px", flexDirection: 'column-reverse' }}
            seatRightStyle={{ paddingTop: "103px" }}
          />
          <TableContainer
            startPosition={sumValuesUntilIndex(tableSizes, 4)}
            up="0"
            down="0"
            left="10"
            right="10"
            width="100px"
            height="550px"
            seatLeftStyle={{ flexDirection: 'column-reverse' }}
          />
          <TableContainer
            startPosition={sumValuesUntilIndex(tableSizes, 5)}
            up="0"
            down="0"
            left="10"
            right="10"
            width="100px"
            height="550px"
            seatLeftStyle={{ flexDirection: 'column-reverse' }}
          />
        </HorizontalContainer>
        <button className={isRunning ? 'running' : 'ready'} onClick={handleClick}>{isRunning ? 'STOP' : 'RUN'}</button>
        <h4><p>Iteration: {iteration}</p><p>Score: {score.toFixed(3)}</p></h4>
    </div>
  );
};

export default WeddingHall;
