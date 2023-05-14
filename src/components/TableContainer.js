import Seats from './Seats';
import Table from './Table';
import VerticalContainer from './UI/VerticalContainer';
import HorizontalContainer from './UI/HorizontalContainer';

const TableContainer = (props) => {
    const startPosition = parseInt(props.startPosition);
    const positionLeft = startPosition;
    const positionUp = positionLeft + parseInt(props.left);
    const positionRight = positionUp + parseInt(props.up);
    const positionDown = positionRight + parseInt(props.right);

    return <HorizontalContainer style={props.tableStyle}>
        <Seats amount={props.left} direction='left' startPosition={positionLeft} style={props.seatLeftStyle} />
        <VerticalContainer>
            <Seats amount={props.up} direction='up' startPosition={positionUp} style={props.seatUpStyle} />
            <Table width={props.width} height={props.height} />
            <Seats amount={props.down} direction='down' startPosition={positionDown} style={props.seatDownStyle} />
        </VerticalContainer>
        <Seats amount={props.right} direction='right' startPosition={positionRight} style={props.seatRightStyle} />
    </HorizontalContainer>
}

export default TableContainer;