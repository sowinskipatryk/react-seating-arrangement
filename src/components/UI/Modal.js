import styles from "./Modal.module.css";

const Modal = (props) => {
  return <div className={styles.modal} onMouseEnter={props.onMouseEnter} onMouseLeave={props.onMouseLeave}><span>{props.guestName}</span><span>{props.seatCost}</span></div>;
};

export default Modal;
