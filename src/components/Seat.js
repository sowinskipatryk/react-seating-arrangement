import styles from "./Seat.module.css";
import { modalActions } from "../store/modalSlice";
import { useDispatch } from "react-redux";
import Modal from "./UI/Modal";
import { useSelector } from "react-redux";
import convert from 'color-convert';



const Seat = (props) => {
  const showNumbers = true;
  const dispatch = useDispatch();
  const modalOpen = useSelector(state => state.modal.modalOpen);
  const position = props.position;
  const guests = useSelector(state => state.tables.guests);
  const guest = guests[position-1];
  const probabilities = useSelector(state => state.tables.probabilities);
  const probabilityValue = probabilities[position-1];
  const [hue, saturation, value] = [probabilityValue * 120, 90, 80];
  const [rVal, gVal, bVal] = convert.hsv.rgb(hue, saturation, value);
  const rgbValue = `rgb(${rVal}, ${gVal}, ${bVal})`;

  const handleOpenModal = () => {
    dispatch(modalActions.openModal(position));
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
      style={{backgroundColor: rgbValue}}
    >
      {showNumbers ? props.position : null}
    </div>
    {modalOpen === position ? <Modal text={`${guest} ${probabilityValue}`} /> : null}
    </div>
  );
};

export default Seat;
