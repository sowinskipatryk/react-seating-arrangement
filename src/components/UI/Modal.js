import styles from "./Modal.module.css";

const Modal = (props) => {
  return <div className={styles.modal}>{props.text}</div>;
};

export default Modal;
