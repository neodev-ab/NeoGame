import React from "react";
import styles from "./gameTable.module.css";
import { Droppable } from "react-beautiful-dnd";
import Card from "./Card";

function GameTable(props) {
  const renderOpponentCards = () => {
    let cards = props.opponentActionCards.map((card, idx) => {
      if (props.roundDone) {
        return (
          <Card
            front
            opponent
            key={idx}
            className={styles.opponent}
            cardId={card}
          ></Card>
        );
      } else if (idx < 2) {
        return (
          <Card
            front
            opponent
            key={idx}
            className={styles.opponent}
            cardId={card}
          ></Card>
        );
      } else {
        return <Card key={idx} className={styles.opponent}></Card>;
      }
    });
    return cards;
  };
  const renderPlayerCards = () => {
    let playerCards = props.playerActionCards;
    //console.log(Object.values(playerCards)[2]);

    return Object.keys(playerCards).length !== 0 ? (
      <>
        {console.log(playerCards)}
        <Card front cardId={playerCards["card_0"].value}></Card>
        <Card front cardId={playerCards["card_1"].value}></Card>

        <Droppable droppableId="pickedCardFirst">
          {provided => (
            <div
              className={styles.frontCard + " " + styles.card}
              ref={provided.innerRef}
              {...provided.droppableProps}
            >
              {Object.keys(playerCards).length > 2 ? (
                <Card
                  key={Object.values(playerCards)[2].id}
                  draggable
                  front
                  dragId={Object.values(playerCards)[2].id}
                  cardId={Object.values(playerCards)[2].value}
                ></Card>
              ) : (
                provided.placeholder
              )}
            </div>
          )}
        </Droppable>
        <Droppable droppableId="pickedCardSecond">
          {provided => (
            <div
              className={styles.frontCard + " " + styles.card}
              ref={provided.innerRef}
              {...provided.droppableProps}
            >
              {Object.keys(playerCards).length > 3 ? (
                <Card
                  key={Object.values(playerCards)[3].id}
                  draggable
                  front
                  dragId={Object.values(playerCards)[3].id}
                  cardId={Object.values(playerCards)[3].value}
                ></Card>
              ) : (
                provided.placeholder
              )}
            </div>
          )}
        </Droppable>
      </>
    ) : null;
  };
  return (
    <div className={styles.theTable}>
      <div className={styles.cardContainer}>
        <div className={styles.cardRow}>{renderOpponentCards()}</div>
        <div className={styles.cardRow}>{renderPlayerCards()}</div>
      </div>
    </div>
  );
}

export default GameTable;
