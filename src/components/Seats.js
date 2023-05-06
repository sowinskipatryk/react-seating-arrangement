import Seat from './Seat';
import styles from './Seats.module.css';

const Seats = (props) => {
    const isVertical = props.direction === 'up' | props.direction === 'down';
    const seats = [];

    for (let i = 1; i <= props.amount; i++) {
      let id = props.startId + i; 
      seats.push(<Seat id={id} key={id} direction={props.direction} />);
    }
    return <div className={`${styles.seats} ${styles[isVertical ? 'seatsVertical' : 'seatsHorizontal']}`}>
        {seats}
    </div>
};

export default Seats;