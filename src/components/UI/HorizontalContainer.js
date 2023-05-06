import styles from './HorizontalContainer.module.css';

const HorizontalContainer = (props) => {
    return <div className={styles.horizontalContainer} style={props.style}>
        {props.children}
    </div>
}

export default HorizontalContainer;