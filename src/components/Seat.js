import styles from "./Seat.module.css";
import { modalActions } from "../store/index";
import { useDispatch } from "react-redux";
import Modal from "./UI/Modal";
import { useSelector } from "react-redux";
import convert from 'color-convert';

const DUMMY_DATA = Array(106).fill().map(() => Math.random().toFixed(2));

const Seat = (props) => {
  const showNumbers = true;
  const dispatch = useDispatch();
  const modalOpen = useSelector(state => state.modalOpen);
  const id = props.id;
  const dataValue = DUMMY_DATA[id-1];
  const [hue, saturation, value] = [dataValue * 120, 90, 80];
  const [rVal, gVal, bVal] = convert.hsv.rgb(hue, saturation, value);
  const rgbValue = `rgb(${rVal}, ${gVal}, ${bVal})`;

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
      style={{backgroundColor: rgbValue}}
    >
      {showNumbers ? props.id : null}
    </div>
    {modalOpen === id ? <Modal text={dataValue} /> : null}
    </div>
  );
};

export default Seat;
