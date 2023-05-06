import styles from './Seat.module.css';

const Seat = (props) => {
    const showNumbers = true;
    return <div className={`${styles.seat} ${styles['seat-'+props.direction]}`}>{showNumbers ? props.id : null}</div>
}

export default Seat;