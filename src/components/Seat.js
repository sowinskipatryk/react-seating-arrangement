import styles from "./Seat.module.css";
import { modalActions } from "../store/modalSlice";
import { useDispatch, useSelector } from "react-redux";
import { useRef } from 'react';
import Modal from "./UI/Modal";
import convert from 'color-convert';


const Seat = (props) => {
  const showNumbers = true;
  const dispatch = useDispatch();
  const modalOpen = useSelector(state => state.modal.modalOpen);
  const timeoutRef = useRef(null);
  const position = props.position;
  const arrangement = useSelector(state => state.tables.arrangement);
  const guestMapping = useSelector(state => state.tables.guestMapping);
  const guest = guestMapping[arrangement[position-1]];
  const seatCosts = useSelector(state => state.tables.seatCosts);
  let seatCost = seatCosts[position-1];
  if (typeof seatCost === 'undefined') {
    seatCost = 1;
  }
  const [hue, saturation, value] = [120 - (120 * seatCost), 90, 80];
  const [rVal, gVal, bVal] = convert.hsv.rgb(hue, saturation, value);
  const rgbValue = `rgb(${rVal}, ${gVal}, ${bVal})`;

  const handleCloseModal = () => {
      dispatch(modalActions.closeModal())
  };

  const handleOpenModal = () => {
    if (timeoutRef.current) {
      clearTimeout(timeoutRef.current);
    };
    dispatch(modalActions.openModal(position));
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
    {modalOpen === position ? <Modal guestName={guest} seatCost={seatCost.toFixed(3)} onMouseEnter={handleOpenModal} onMouseLeave={handleCloseModal} /> : null}
    </div>
  );
};

export default Seat;
