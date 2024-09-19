import React, { useState, useEffect, useRef } from 'react';
import { View, Text, Button, StyleSheet, Animated, Easing, Image, TouchableOpacity } from 'react-native';
import { BarCodeScanner } from 'expo-barcode-scanner';
import axios from 'axios';

const DetectionScreen = ({ navigation }) => {
  const [barcode, setBarcode] = useState('');
  const [hasPermission, setHasPermission] = useState(null);
  const [scanned, setScanned] = useState(false);
  const [product, setProduct] = useState(null);
  const [price, setPrice] = useState(0); 
  const animatedValue = useRef(new Animated.Value(0)).current;

  useEffect(() => {
    const getBarCodeScannerPermissions = async () => {
      const { status } = await BarCodeScanner.requestPermissionsAsync();
      setHasPermission(status === 'granted');
    };

    getBarCodeScannerPermissions();
    startLineAnimation(); 
  }, []);

  const startLineAnimation = () => {
    Animated.loop(
      Animated.sequence([
        Animated.timing(animatedValue, {
          toValue: 1,
          duration: 2000,
          easing: Easing.linear,
          useNativeDriver: true,
        }),
        Animated.timing(animatedValue, {
          toValue: 0,
          duration: 2000,
          easing: Easing.linear,
          useNativeDriver: true,
        }),
      ]),
    ).start();
  };

  const handleBarCodeScanned = ({ type, data }) => {
    if (!scanned) {
      setScanned(true);
      setBarcode(data);
      detectProduct(data);
    }
  };

  const detectProduct = async (barcode) => {
    try {
      const response = await axios.post('http://localhost:8000/api/detect/', { barcode });
      setProduct(response.data);
      setPrice(response.data.price); 
    } catch (error) {
      console.error(error);
    }
  };

  const increasePrice = () => {
    setPrice(prevPrice => prevPrice + 1); 
  };

  const decreasePrice = () => {
    setPrice(prevPrice => (prevPrice > 0 ? prevPrice - 1 : 0)); 
  };

  if (hasPermission === null) {
    return <Text>Requesting for camera permission</Text>;
  }
  if (hasPermission === false) {
    return <Text>No access to camera</Text>;
  }

  const translateY = animatedValue.interpolate({
    inputRange: [0, 1],
    outputRange: [0, 250], 
  });

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Détecter produit</Text>

      {!scanned ? (
        <View style={styles.cameraContainer}>
          <BarCodeScanner
            onBarCodeScanned={handleBarCodeScanned}
            style={StyleSheet.absoluteFillObject}
          />
          
          <View style={styles.overlay}>
            <View style={styles.cornerTopLeft} />
            <View style={styles.cornerTopRight} />
            <View style={styles.cornerBottomLeft} />
            <View style={styles.cornerBottomRight} />
            
            <Animated.View style={[styles.redLine, { transform: [{ translateY }] }]} />
          </View>
        </View>
      ) : (
        <View style={styles.formContainer}>
          <Button title="Scanner encore" onPress={() => setScanned(false)} />
          
          <Button title="Détection" onPress={() => detectProduct(barcode)} />
          
          {product && (
            <View style={styles.productInfo}>
              {product.image && (
                <Image 
                  source={{ uri: product.image }} 
                  style={styles.productImage} 
                  resizeMode="contain"
                />
              )}

              <Text>Produit détecté :</Text>
              <Text>Titre : {product.title}</Text>
              
              <View style={styles.priceContainer}>
                <TouchableOpacity style={styles.priceButton} onPress={decreasePrice}>
                  <Text style={styles.buttonText}>-</Text>
                </TouchableOpacity>
                
                <Text style={styles.priceText}>Prix : {price} USD</Text>
                
                <TouchableOpacity style={styles.priceButton} onPress={increasePrice}>
                  <Text style={styles.buttonText}>+</Text>
                </TouchableOpacity>
              </View>
            </View>
          )}
        </View>
      )}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
    justifyContent: 'center',
  },
  title: {
    fontSize: 24,
    marginBottom: 20,
  },
  cameraContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  overlay: {
    position: 'absolute',
    width: 250,
    height: 250,
    borderColor: 'white',
    justifyContent: 'center',
    alignItems: 'center',
  },
  cornerTopLeft: {
    position: 'absolute',
    top: 0,
    left: 0,
    width: 30,
    height: 30,
    borderColor: 'blue',
    borderLeftWidth: 4,
    borderTopWidth: 4,
  },
  cornerTopRight: {
    position: 'absolute',
    top: 0,
    right: 0,
    width: 30,
    height: 30,
    borderColor: 'blue',
    borderRightWidth: 4,
    borderTopWidth: 4,
  },
  cornerBottomLeft: {
    position: 'absolute',
    bottom: 0,
    left: 0,
    width: 30,
    height: 30,
    borderColor: 'blue',
    borderLeftWidth: 4,
    borderBottomWidth: 4,
  },
  cornerBottomRight: {
    position: 'absolute',
    bottom: 0,
    right: 0,
    width: 30,
    height: 30,
    borderColor: 'blue',
    borderRightWidth: 4,
    borderBottomWidth: 4,
  },
  redLine: {
    width: '100%',
    height: 2,
    backgroundColor: 'red',
    position: 'absolute',
    top: 0,
  },
  formContainer: {
    padding: 20,
    backgroundColor: 'white',
    borderRadius: 10,
    elevation: 5,
  },
  productInfo: {
    marginTop: 20,
  },
  productImage: {
    width: 150,
    height: 150,
    marginBottom: 20,
  },
  priceContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    marginTop: 10,
  },
  priceButton: {
    backgroundColor: '#007bff',
    padding: 10,
    borderRadius: 5,
    marginHorizontal: 10,
  },
  buttonText: {
    color: 'white',
    fontSize: 18,
  },
  priceText: {
    fontSize: 18,
  },
});

export default DetectionScreen;
