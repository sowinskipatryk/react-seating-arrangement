import styles from './Table.module.css';

const Table = (props) => {
    const divStyle = {
        width: props.width,
        height: props.height,
    }
    return <div className={styles.table} style={divStyle}></div>
}

export default Table;