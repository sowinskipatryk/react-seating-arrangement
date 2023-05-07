import Seats from './Seats';
import Table from './Table';
import VerticalContainer from './UI/VerticalContainer';
import HorizontalContainer from './UI/HorizontalContainer';

const TableContainer = (props) => {
    const startId = parseInt(props.startId);
    const idLeft = startId;
    const idUp = idLeft + parseInt(props.left);
    const idRight = idUp + parseInt(props.up);
    const idDown = idRight + parseInt(props.right);

    return <HorizontalContainer style={props.tableStyle}>
        <Seats amount={props.left} direction='left' startId={idLeft} style={props.seatLeftStyle} />
        <VerticalContainer>
            <Seats amount={props.up} direction='up' startId={idUp} style={props.seatUpStyle} />
            <Table width={props.width} height={props.height} />
            <Seats amount={props.down} direction='down' startId={idDown} style={props.seatDownStyle} />
        </VerticalContainer>
        <Seats amount={props.right} direction='right' startId={idRight} style={props.seatRightStyle} />
    </HorizontalContainer>
}

export default TableContainer;