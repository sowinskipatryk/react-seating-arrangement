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
    return <HorizontalContainer style={props.style}>
        <Seats amount={props.left} direction='left' startId={idLeft} />
        <VerticalContainer>
            <Seats amount={props.up} direction='up' startId={idUp} />
            <Table width={props.width} height={props.height} />
            <Seats amount={props.down} direction='down' startId={idDown} />
        </VerticalContainer>
        <Seats amount={props.right} direction='right' startId={idRight} />
    </HorizontalContainer>
}

export default TableContainer;