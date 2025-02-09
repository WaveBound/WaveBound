// Track user presence
const userRef = database.ref(`users/${userId}`);
const connectedRef = database.ref('.info/connected');

connectedRef.on('value', (snap) => {
  if (snap.val() === true) {
    // When user connects
    userRef.onDisconnect().remove();
    userRef.set(true);
    
    // Increment active users
    activeUsersRef.transaction((currentCount) => {
      return (currentCount || 0) + 1;
    });
  }
});
