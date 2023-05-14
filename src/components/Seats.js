import Seat from './Seat';
import styles from './Seats.module.css';

const Seats = (props) => {
    const isVertical = props.direction === 'up' | props.direction === 'down';
    const seats = [];

    for (let i = 1; i <= props.amount; i++) {
      let position = props.startPosition + i; 
      seats.push(<Seat position={position} key={position} direction={props.direction} />);
    }
    return <div className={`${styles.seats} ${styles[isVertical ? 'seatsVertical' : 'seatsHorizontal']}`} style={props.style}>
        {seats}
    </div>
};

export default Seats;