import React from 'react';
import { View, Text, Button, StyleSheet } from 'react-native';

const HomeScreen = ({ navigation }) => {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>Bienvenue sur G-Paie!</Text>
      <Button
        title="Scanner les produits"
        onPress={() => navigation.navigate('Detection')}
      />
      <Button
        title="Historique d'achats"
        onPress={() => navigation.navigate('History')}
      />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center'
  },
  title: {
    fontSize: 24,
    marginBottom: 20
  }
});

export default HomeScreen;
