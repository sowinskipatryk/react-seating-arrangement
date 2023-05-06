import styles from './VerticalContainer.module.css';

const VerticalContainer = (props) => {
    return <div className={styles.verticalContainer}>
        {props.children}
    </div>
}

export default VerticalContainer;