import styles from "./Seat.module.css";
import { modalActions } from "../store/index";
import { useDispatch } from "react-redux";
import Modal from "./UI/Modal";
import { useSelector } from "react-redux";

const DUMMY_DATA = Array.from({ length: 102 }, (_, i) => i * 0.1);

const Seat = (props) => {
  const showNumbers = true;
  const dispatch = useDispatch();
  const modalOpen = useSelector(state => state.modalOpen);
  const id = props.id;

  const handleOpenModal = () => {
    dispatch(modalActions.openModal(id));
  };

  const handleCloseModal = () => {
    dispatch(modalActions.closeModal());
  };
  return (
    <div className={styles.seatContainer}>
    <div
      className={`${styles.seat} ${styles["seat-" + props.direction]}`}
      onMouseEnter={handleOpenModal}
      onMouseLeave={handleCloseModal}
    >
      {showNumbers ? props.id : null}
    </div>
    {modalOpen === id ? <Modal text={DUMMY_DATA[id-1].toFixed(2)} /> : null}
    </div>
  );
};

export default Seat;
