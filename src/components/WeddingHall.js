import TableContainer from './TableContainer';
import HorizontalContainer from './UI/HorizontalContainer';
import VerticalContainer from './UI/VerticalContainer';

const WeddingHall = () => {
    return <div>
        <VerticalContainer>
            <TableContainer startId="0" up="6" down="0" left="0" right="0" width="400px" height="100px" style={{translate: '-32%'}} />
            <HorizontalContainer>
                <TableContainer startId="6" up="0" down="0" left="11" right="11" width="100px" height="600px" />
                <TableContainer startId="28" up="0" down="0" left="8" right="7" width="100px" height="450px" />
                <TableContainer startId="43" up="0" down="0" left="7" right="8" width="100px" height="450px" />
                <TableContainer startId="58" up="0" down="0" left="11" right="11" width="100px" height="600px" />
                <TableContainer startId="80" up="0" down="0" left="11" right="11" width="100px" height="600px" />
            </HorizontalContainer>
        </VerticalContainer>
    </div>
}

export default WeddingHall;